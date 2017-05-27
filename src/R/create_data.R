library(dplyr)

create_data_num <- 10000
time_range <- 100
anomaly_num <- 100
period_num <- 6

# Creat Data
white_noize <- as.integer(rnorm(time_range)*10)
df = data.frame(white_noize)
for(i in 2:create_data_num){
  white_noize <- as.integer(rnorm(time_range)*10)
  #period <-rep(c(15,rep(0,time_range/period_num-1)),period_num)
  #df[,i] <- white_noize + period[0:300]
  df[,i] <- white_noize
  #plot(df[,i],type="l")
}

# Anomaly Data
Anomaly <- as.integer(runif(anomaly_num, min = 60, max = 100))
target_index <- as.integer(runif(anomaly_num, min = 1, max = time_range))
for(i in 1:anomaly_num){
  df[target_index[i],i] <- Anomaly[i]
  #plot(df[,i],type="l")
}

# OutPut
#out <- file("./data.txt", "w")
out <- file("./data_ft.txt", "w")
#out <- file("./data_ft_test.txt", "w")
for(i in 1:create_data_num) {
  if(i <= anomaly_num) writeLines(text = sprintf("__label__1"), con = out, sep=" ")
  else writeLines(text = sprintf("__label__2"), con = out, sep=" ")
  for(j in 1:time_range){
    if(j == time_range) writeLines(text = sprintf(toString(df[,i][j])), con = out, sep="\n")
    #else writeLines(text = sprintf(toString(df[,i][j])), out, sep=",")
    else writeLines(text = sprintf(toString(df[,i][j])), out, sep=" ")
  }
}
close(out)
