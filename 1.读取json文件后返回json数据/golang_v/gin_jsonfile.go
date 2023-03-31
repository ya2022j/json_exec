package main

// dt.json ==>string==> json array==>
// GoLang结构体解析多维复杂json  https://blog.csdn.net/qq_38883889/article/details/109559380

import (
	"encoding/json"
	"fmt"
	"io/ioutil"

	"github.com/gin-gonic/gin"
	"github.com/tidwall/gjson"
)

func CheckError(err error) {
	if err != nil {
		panic(err)
	}
}

// 嵌套结构体
type Top struct {
	List []List `json:"list"`
}

type List struct {
	Id       int64      `json:"id"`
	Value    int64      `json:"value"`
	Label    string     `json:"label"`
	Children []Children `json:"children"`
}

type Children struct {
	Id      int64  `json:"id"`
	Value   int64  `json:"value"`
	Label   string `json:"label"`
	ZipCode string `json:"zip_code"`
}

func ReturnJSONString(container string, item string) string {
	json_ret := gjson.Get(container, item)
	value := json_ret.String()
	return value
}

func readjsonfile(jsonfile string) (result interface{}) {

	content, err := ioutil.ReadFile(jsonfile)
	CheckError(err)

	// var str_content string
	string_result := string(content)

	// for_gin_json := map[string]interface{}{"json_result": result}

	//string--->json array

	// var data Nikki225
	var data Top
	// var data []map[string]interface{}
	if err := json.Unmarshal([]byte(string_result), &data); err == nil {

		return data
		//fmt.Println(dat["status"])
	} else {
		fmt.Println(err)
	}
	return

}

func main() {

	result := readjsonfile("dt.json")
	router := gin.Default()

	router.GET("/", func(c *gin.Context) {
		c.PureJSON(200, result)

	})

	router.Run(":8888")

}
