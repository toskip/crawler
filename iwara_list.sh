for i in {0..99}
do
  date +'%Y-%m-%d %H:%M:%S'
  echo start batch $i
  for j in {0..19}
  do
    k=$((i*20+j))
    echo https://ecchi.iwara.tv/videos?page=$k
    curl -s -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36' -O https://ecchi.iwara.tv/videos?page=$k &
  done
  wait
  echo finish batch $i
done
