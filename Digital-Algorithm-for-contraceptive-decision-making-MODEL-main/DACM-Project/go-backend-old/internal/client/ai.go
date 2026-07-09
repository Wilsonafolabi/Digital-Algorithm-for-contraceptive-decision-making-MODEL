package client

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
	"dacm-go/internal/models"
)

type AI struct {
	url    string
	client *http.Client
}

func New(url string) *AI {
	return &AI{url: url, client: &http.Client{Timeout: 30 * time.Second}}
}

func (a *AI) Ask(ctx context.Context, r models.Req) (*models.Res, error) {
	body, _ := json.Marshal(r)
	req, _ := http.NewRequestWithContext(ctx, "POST", a.url+"/api/v1/generate", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	res, err := a.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		return nil, fmt.Errorf("AI status %d", res.StatusCode)
	}
	var out models.Res
	return &out, json.NewDecoder(res.Body).Decode(&out)
}