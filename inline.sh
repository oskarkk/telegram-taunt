#!/bin/bash

# Telegram bot's token
botToken=""
# bot API URL
tgURL="https://api.telegram.org/bot"$botToken"/"
# taunt local directory
audioPath="/home/oskark/public_html/taunt/"
# taunt http URL
httpURL="https://oskark.pl/taunt/"

# get the list of all files, without whole "/home/..." path
audioList=`ls -v "$audioPath"* | sed 's/.*\///g'`

while true

# for benchmarking, to see how often requests should be made
echo `date +%s`

# get the first of the unread updates (or nothing)
json=$(curl -s $tgURL"getUpdates?limit=1")

# while there are any updates
while (( "`python3 tgjson.py "$json" if_results`" == 1 ))
do
  # format reply for debugging
  python3 tgjson.py "$json" pretty

  # get needed data from JSON
  query=`python3 tgjson.py "$json" inline`
  inline_id=`python3 tgjson.py "$json" inline_id`
  update_id=`python3 tgjson.py "$json" update_id`
  # for debug
  #echo $query $inline_id

  if [ -n "$query" ] # not null
  then
    # prepare answer to the inline query
    answer=`python3 tgpath.py "$inline_id" "$query" "$httpURL" "$audioList"`
    if [ -n "$answer" ]
    then
      python3 tgjson.py "$answer" pretty # for debug
      # send the answer
      result=$(curl -sH "Content-Type: application/json" -d "$answer" $tgURL"answerInlineQuery")
      # show the result
      python3 tgjson.py "$result" pretty
    fi
  fi

  # get the next update (or nothing)
  json=`curl -s $tgURL"getUpdates?limit=1&offset="$((update_id + 1))`

done

sleep 1 # wait
done
