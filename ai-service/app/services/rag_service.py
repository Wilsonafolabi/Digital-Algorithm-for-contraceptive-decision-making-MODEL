import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class RAGService:
    def __init__(self):
        self.embed = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.Client(Settings(is_persistent=True, persist_directory="./chroma_db"))
        self.col = self.client.get_or_create_collection(name="who_mec", metadata={"hnsw:space":"cosine"})
        self._seed()

    def _seed(self):
        if self.col.count() == 0:
            docs = [
                {"id":"m1","t":"Combined - Hypertension","c":"WHO MEC 3/4","d":"BP≥140/90: Cat3. BP≥160/100: Cat4. Avoid estrogen. Use progestin-only."},
                {"id":"m2","t":"Progestin-Only - Hypertension","c":"WHO MEC 1","d":"Safe for all hypertension levels. No restriction."},
                {"id":"m3","t":"Smoking + Age >35","c":"WHO MEC 4","d":"Unacceptable CV risk with combined methods. Strictly avoid."},
                {"id":"m4","t":"Migraine with Aura","c":"WHO MEC 4","d":"Absolute contraindication for estrogen due to stroke risk."},
                {"id":"m5","t":"Breastfeeding <6 weeks","c":"WHO MEC 3","d":"Combined pills not recommended. Progestin-only methods are Cat 1 (safe)."},
                {"id":"m6","t":"Diabetes with complications","c":"WHO MEC 3","d":"Combined methods Cat 3. Progestin-only or copper IUD preferred (Cat 1/2)."},
                {"id":"m7","t":"History of DVT/PE","c":"WHO MEC 4","d":"Estrogen strictly contraindicated. Use progestin-only, IUD, or barrier methods."},
                {"id":"m8","t":"Obesity (BMI ≥30)","c":"WHO MEC 2","d":"Combined pills Cat 2. No restriction for progestin-only or IUDs."}
            ]
            txts = [f"{d['t']}: {d['d']}" for d in docs]
            self.col.add(ids=[d["id"] for d in docs], embeddings=self.embed.encode(txts).tolist(), documents=txts, metadatas=[{"title":d["t"],"category":d["c"]} for d in docs])
            print(f"✅ Seeded {len(docs)} contraceptive guidelines")

    def search(self, q: str, p: dict, k: int = 3) -> List[Dict]:
        # Build context from NEW clinical profile structure
        conditions = []
        if p.get("hypertension"): conditions.append("hypertension")
        if p.get("diabetes"): conditions.append("diabetes")
        if p.get("history_of_clots"): conditions.append("blood clots history")
        if p.get("breastfeeding"): conditions.append("breastfeeding")
        if p.get("migraines") == "with_aura": conditions.append("migraine with aura")
        if p.get("smoking_status") == "smoker": conditions.append("smoker")
        
        ctx = f"Age {p.get('age', 'N/A')}, Conditions: {', '.join(conditions) if conditions else 'None'}. Query: {q}"
        
        res = self.col.query(query_embeddings=[self.embed.encode([ctx])[0].tolist()], n_results=k, include=["documents","metadatas","distances"])
        out = []
        if res["documents"]:
            for i, doc in enumerate(res["documents"][0]):
                out.append({
                    "title": res["metadatas"][0][i]["title"],
                    "category": res["metadatas"][0][i]["category"],
                    "content": doc,
                    "relevance_score": round(1/(1+res["distances"][0][i]), 2)
                })
        return out