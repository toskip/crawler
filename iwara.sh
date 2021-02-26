#列表页
mkdir list
cd list
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

#提取链接
mkdir content
grep -oE '<h3 class="title"><a href="(.*)"'  * | awk -F\" '{print $4}' > ./content/seed.txt

#详情页
cd content
for i in {0..14288}
do
  date +'%Y-%m-%d %H:%M:%S'
  echo start batch $i
  for j in {0..4}
  do
    k=$((i*5+j))
    url=https://ecchi.iwara.tv$(sed -n "${k},${k}p" seed.txt)
    echo $url
    curl -s -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36' -O $url &
  done
  wait
  #抓太快会封一个小时ip
  sleep 5
  echo finish batch $i
done
