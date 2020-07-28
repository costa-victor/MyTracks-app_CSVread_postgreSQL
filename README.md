# Intro
If you want export your route from MyTracks app, read them and insert them on postgreSQL database, this can help you :)

# How it works
## App
After install [MyTracks](https://play.google.com/store/apps/details?id=com.zihua.android.mytracks&hl=en_US) app, a powerful application to keep track of your route while you go around and also add some markers on map.
You can export your route into a CSV File.

![img1](https://lh3.googleusercontent.com/1l4ZrFs_wRppdHAtTogDT_CZ5ESFKBQ_dC1nOLQglEypt28xELkrngTvoDwSYk3SRQ=w1366-h664-rw)
![img2](https://lh3.googleusercontent.com/ecrJKLgW4IhqBPJXlm6E7u7AM8CDfa4g7fyBz1NSzxy35ebu1hNrhVYDk3j7b52u9_rK=w1366-h664-rw)

## Python code
This code read the CSV File, applies a filter on markers, that when a marker in the CSV file is close enough to a marker in the database, based on the **radius** parameter, it will not be added to the database.
After filtering, insert the data into your postgreSQL database.
