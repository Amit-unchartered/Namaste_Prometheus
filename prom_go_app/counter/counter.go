package main

//prometheus is the core instrumentation package, this provides metrics primitives to instrument code and also offers registry for metrics
//promhttp -> helps us with the creation of http.handler instances to expose prometheus metrics via http, with this we can be able to expose this metrics on HTTp.
//promauto -> provides metric constructors with automatic resgistration.

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var REQUEST_COUNT = promauto.NewCounter(prometheus.CounterOpts{
	Name: "go_app_requests_count",
	Help: "Total App HTTP Requests count.",
})

func main() {
	//start the application
	startMyApp()
}

func startMyApp() {
	router := mux.NewRouter()
	router.HandleFunc("/birthday/{name}", func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		name := vars["name"]
		greetings := fmt.Sprintf("Happy Birthday %s :)", name)
		w.Write([]byte(greetings))

		REQUEST_COUNT.Inc()
	}).Methods("GET")

	log.Println("starting the application server...")
	router.Path("/metrics").Handler(promhttp.Handler()) //this will expose the metrics at localhost:8000/metrics
	http.ListenAndServe(":8000", router)
}
