# toc-chatbot: 道德小測驗




## Setup

### Prerequisite
* Python 3.6
* Line App
* HTTPS Server

#### Install Dependency
```sh
pip install -r requirement.txt
```

#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python app.py
```

## Finite State Machine
![fsm](https://i.imgur.com/Dya0r6V.png)



## Usage
The initial state is set to `user`.
在任何state輸入restart會回到start state
* state: user
    * Input: "start"
	    * state: start
		* Reply: "有一天當你走在路上，看到一個老爺爺掉進河裡，請問你會怎麼做?"
		* button: "跳下去救他", "我不會游泳沒辦法救"
		
		    * Input: "跳下去救他"
		        * state: save
		        * Reply: "將老爺爺救起來後，老爺爺決定給你一筆錢是否接受"
		        * button: "竟然你都這麼說了(默默伸手)", "我幫助你並不是為了錢"
		            
                    * Input: "竟然你都這麼說了(默默伸手)"
                        * state: thousand
                        * Reply: "結果老爺爺給你一千塊!!"
                        * button: "太少了，要再多一點", "收起來說謝謝"

                            * Input: "太少了，要再多一點"
                                * state: greedy
                                * Reply: "被老爺爺打，說你這個貪心的人(遊戲結束)"(回到user state)
                                 
                            * Input: "收起來說謝謝"
                                * state: notbad
                                * Reply: "恭喜你救了人也得到回報(遊戲結束)"(回到user state)
                       
                    * Input: "我幫助你並不是為了錢"
                        * state: compensate
                        * Reply: "不然我給你其他補償?"
                        * button: "好啊", "沒關係不用"
                        
                            * Input: "好啊"
                                * state: daughter
                                * Reply: "我決定將我貌美如花的女兒許配給你"
                                * button: "謝謝岳父大人", "我先看看你女兒", "不用了，因為我是gay"
                                
                                    * Input: "謝謝岳父大人"
                                        * state: happy
                                        * Reply: "從此以後和老婆過著幸福快樂的生活(遊戲結束)"(回到user state)
                                    * Input: "我先看看你女兒"
                                        * state: ugly
                                        * Reply: "結果發現他女兒真的是如花(遊戲結束)"(回到user state)
                                    * Input: "不用了，因為我是gay"
                                        * state: gay
                                        * Reply: "老爺爺以飛快的速度逃離現場(遊戲結束)"(回到user state)
                            * Input: "沒關係不用"
                                * state: recompensate
                                * Reply: "結果聽說她女兒貌美如花，是否想重新選擇?"
                                * button: "是，我想脫魯", "否"
                                    * Input: "是，我想脫魯"
                                        * state: compensate
                                    * Input: "否"
                                        * state: goodman
                                        * Reply: "你是個不求回報的大善人(遊戲結束)"(回到user state)
		    * Input: "我不會游泳沒辦法救"
		        * state: "swimmingring"
		        * Reply: "但是旁邊剛好有游泳圈欸，你確定不救?"
		        * button: "當然救", "有急事，應該會有人救吧"
		            
                    * Input: "當然救"
                        * state: save
                        
                    * Input: "有急事，應該會有人救吧"
                        * state: guilty
                        * Reply: "結果看到新聞報導那位老爺爺溺死在河中請問你會愧疚嗎"
                        * button: "當然會愧疚", "雖然他死了，但不是我的錯"
                        
                            * Input: "當然會愧疚"
                                * state: reriverfromguilty
                                * Reply: "如果可以重來你還願意嗎"
                                * button: "我願意", "還是算了"
                                    * Input: "我願意"
                                        * state: start
                                         
                                    * Input: "還是算了"
                                        * state: selfish
                                        * Reply: "你是個自私的人，丟個游泳圈有那麼難嗎(遊戲結束)"(回到user state)
                            * Input: "雖然他死了，但不是我的錯"
                                * state: encounter
                                * Reply: "過了幾天去河邊玩，不小心掉進去河裡，但路過的人也都不救你，你會恨他們嗎?"
                                * button: "當然會恨", "我不會恨他們"
                                    * Input: "當然會恨"
                                        * state: bad
                                        * Reply: "可是你當初也是這樣啊~(遊戲結束)"(回到user state)
                                        
                                    * Input: "我不會恨他們"
                                        * state: reriver
                                        * Reply: "如果可以重來你還願意嗎"
                                        * button: "我願意", "還是算了"
                                            * Input: "我願意"
                                                * state: start
                                                 
                                            * Input: "還是算了"
                                                * state: gameover
                                                * Reply: "隨後慢慢沉入河裡(遊戲結束)"(回到user state) 

	* Input: "fsm"
		* state: fsm
		* Reply: ![fsm](https://i.imgur.com/Dya0r6V.png)(回到user state)

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz

## Reference
https://github.com/ire33164/Girlfriend_chatbot
