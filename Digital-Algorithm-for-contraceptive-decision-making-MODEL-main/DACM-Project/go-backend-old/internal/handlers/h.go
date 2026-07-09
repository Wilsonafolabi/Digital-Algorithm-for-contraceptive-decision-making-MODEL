package handlers

import (
	"dacm-go/internal/client"
	"dacm-go/internal/models"

	"github.com/gin-gonic/gin"
)

type H struct {
	AI *client.AI
}

func (h *H) Advice(c *gin.Context) {
	var r models.Req
	if err := c.ShouldBindJSON(&r); err != nil {
		c.JSON(400, gin.H{"err": err.Error()})
		return
	}
	if r.UserProfile.Age < 18 {
		c.JSON(200, models.Res{
			Route: models.Route{
				ToCounselor: true,
				Reason:      "Minors require direct counseling per WHO guidelines.",
				Endpoint:    "/api/v1/counseling/book",
			},
			Ans:  "Please book a session with a certified counselor.",
			Safe: models.Safe{Flagged: true, Action: "consult_provider"},
		})
		return
	}
	res, err := h.AI.Ask(c.Request.Context(), r)
	if err != nil {
		c.JSON(503, gin.H{"err": err.Error()})
		return
	}
	res.Route = models.Route{ToCounselor: false}
	c.JSON(200, res)
}
