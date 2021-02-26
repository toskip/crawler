#列表页
mkdir list
cd list
#batch数
for i in {0..99}
do
  date +'%Y-%m-%d %H:%M:%S'
  echo start batch $i
  #并发数
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
for i in {0..7145}
do
  date +'%Y-%m-%d %H:%M:%S'
  echo start batch $i
  for j in {0..9}
  do
    k=$((i*10+j))
    url=https://ecchi.iwara.tv$(sed -n "${k},${k}p" seed.txt)
    echo $url
    curl -s -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36' -O $url &
  done
  wait
  #抓太快会封一个小时ip，具体阈值应该在这附近，应该有两个状态，第一个状态会限制访问频率，第二个直接拉黑，这个频率刚好没进入第一个
  sleep 3
  echo finish batch $i
done
