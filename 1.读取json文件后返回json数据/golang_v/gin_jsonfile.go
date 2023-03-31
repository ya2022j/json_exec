package main

// dt.json ==>
// GoLang结构体解析多维复杂json  https://blog.csdn.net/qq_38883889/article/details/109559380
import (
	"io/ioutil"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/tidwall/gjson"
)

func CheckError(err error) {
	if err != nil {
		panic(err)
	}
}

func ReadJsonfile(filename string) string {
	content, err := ioutil.ReadFile(filename)
	CheckError(err)
	return string(content)
}


func ReturnJSONString(container string, item string) string {
	json_ret := gjson.Get(container, item)
	value := json_ret.String()
	return value
}

func main() {
	ret := ReadJsonfile("dt.json")
	router := gin.Default()
	router.GET("/", func(c *gin.Context) {
		data := map[string]interface{}{

			"username": ReturnJSONString(ret, "username"),
			"age":      ReturnJSONString(ret, "age"),
		}
		c.JSON(http.StatusOK, data)
	})
	router.Run(":8888")
}
