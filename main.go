package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os/exec"
	"strings"
	"time"
)

type Settings struct {
	ScriptLocation string
	ResourceLock   bool
}

// @dis whole thing can be better.
func (s *Settings) startJob() {
	if c, err := exec.Command("python", s.ScriptLocation).CombinedOutput(); err != nil {
		log.Fatal(err)
	} else {
		fmt.Printf("%s\n", c)
	}
}

func (s *Settings) runScript(w http.ResponseWriter, r *http.Request) {
	go func() {
		free := 0
		for free == 0 {
			if !s.ResourceLock {
				s.ResourceLock = true
				s.startJob()
				s.ResourceLock = false
				free = 1
			}
			time.Sleep(1 * time.Second)
		}
	}()

}

func (s *Settings) health(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("healthy"))
}

func main() {
	port := flag.Int("port", 9090, "port for server to start on")
	fsLocation := *flag.String("ds", "download.py", "download script to be ran")

	if !strings.Contains(fsLocation, ".py") {
		panic("invalid script, script must be python")
	}

	settings := &Settings{
		ScriptLocation: fsLocation,
		ResourceLock:   false,
	}

	http.HandleFunc("/", settings.runScript)
	http.HandleFunc("/health", settings.health)

	s := fmt.Sprintf(":%v", *port)

	err := http.ListenAndServe(s, nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
