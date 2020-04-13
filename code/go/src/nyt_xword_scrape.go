package main

import (
	"database/sql"
	"errors"
	//"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os/exec"
	"strconv"
	"sync"

	_ "github.com/mattn/go-sqlite3"
)

const cookieDBOrig = "/home/peter/.mozilla/firefox/tront8x1.default/cookies.sqlite"
const cookieDB = "/tmp/cookies.sqlite"
const testURL = "https://www.nytimes.com/svc/crosswords/v2/puzzle/1285.puz"

func errCheck(e error) {
	if e != nil {
		log.Print(e)
	}
}

func getNYTCookies() []map[string]string {
	var cookies []map[string]string

	cmd := exec.Command("cp " + cookieDBOrig + " " + cookieDB)
	err := cmd.Run()
	errCheck(err)

	db, err := sql.Open("sqlite3", cookieDB)
	errCheck(err)

	// mozilla updated Firefox and now this SQL request no longer works
	rows, err := db.Query("SELECT name,value FROM moz_cookies WHERE baseDomain=='nytimes.com';")
	errCheck(err)

	var name string
	var value string

	for rows.Next() {
		rows.Scan(&name, &value)

		cookie := map[string]string{"name": name, "value": value}
		cookies = append(cookies, cookie)
	}

	return cookies
}

func reqNYTWithCookies(url string, cookies []map[string]string) (b []byte, err error) {
	req, err := http.NewRequest("GET", url, nil)
	errCheck(err)

	for i := range cookies {
		cookie := cookies[i]
		req.AddCookie(&http.Cookie{Name: cookie["name"], Value: cookie["value"]})
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	errCheck(err)

	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		err = errors.New(url +
			"\nresp.StatusCode: " + strconv.Itoa(resp.StatusCode))
		return
	}

	return ioutil.ReadAll(resp.Body)
}

func formXwordURL(i int) string {
	baseURL := "https://www.nytimes.com/svc/crosswords/v2/puzzle/"
	return baseURL + strconv.Itoa(i) + ".puz"
}

func process(iStart int, blockSize int, cookies []map[string]string, saveDir string, wg *sync.WaitGroup) {
	for i := iStart; i <= (iStart + blockSize); i++ {
		data, err := reqNYTWithCookies(formXwordURL(i), cookies)
		errCheck(err)

		if err == nil {
			ioutil.WriteFile(saveDir+strconv.Itoa(i)+".puz", data, 0644)
		}
	}

	wg.Done()
}

func main() {
	nytCookies := getNYTCookies()

	saveDir := "/home/peter/Junkspace/nyt_xword/data/puz/"
	//nWorkers := 100
	nPuzzles := 30000
	blockSize := 300

	var wg sync.WaitGroup
	for i := 1; i <= nPuzzles; i += blockSize {
		//if i+blockSize > nPuzzles {
		//	blockSize := nPuzzles - i
		//	wg.Add(1)
		//	go process(i, blockSize, nytCookies, saveDir, &wg)
		//}

		wg.Add(1)
		go process(i, blockSize, nytCookies, saveDir, &wg)
	}

	wg.Wait()
}
