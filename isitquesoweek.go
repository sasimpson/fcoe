package main

import (
    "fmt"
    "time"
    "flag"
)

func IsQuesoWeek(day time.Time) (bool) {
    dow := int(day.Weekday())
    bow := day.AddDate(0, 0, -(dow))
    for bow.Month() == day.Month() {
        bow = bow.AddDate(0,0,-7)
    }

    queso_week_start := bow.AddDate(0,0,14)
    queso_week_end := queso_week_start.AddDate(0,0,8)

    if day.After(queso_week_start) && day.Before(queso_week_end) {
        return true
    } else {
        return false
    }
}

func main() {
    const layout = "Jan 02, 2006"
    all := flag.Bool("a", false, "shows all days of the year and which fall in queso week")
    flag.Parse()

    if *all {
        this_year := time.Now().Year()
        for d := time.Date(this_year,1,1,0,0,0,0,time.Local); d.Before(time.Date(this_year+1,1,1,0,0,0,0,time.Local)); d = d.AddDate(0,0,1) {
            fmt.Printf("%s: %t\n", d.Format(layout), IsQuesoWeek(d))
        }
    } else {
        if IsQuesoWeek(time.Now()) {
            fmt.Printf("Yep!")
        } else {
            fmt.Printf("Nope")
        }
    }
}
