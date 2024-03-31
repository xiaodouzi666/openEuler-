# openEuler挑战赛说明文档

接续AtomGit仓库中的内容，这里提出3月份EUR平台炸了之后本地构建的所有操作的内容，以及比赛要求的“在系统上完成对应框架软件包安装部署以及实现推理应用”的实现过程，以及详细说明。
另外，附上在本地服务器上构建的所有新增的源码包、rpm包、spec文件等相关所有代码以及内容。

## 代码说明

**rpmbuild文件夹**中，包含了所有新构建过程中的源码包、spec，以及最后构建好的rpm包。

**infer-apps文件夹**中，包含了AI推理应用的相关代码文件。

# EUR平台炸了之后的操作
首先，对于已经构建好的软件包，我做了安装部署操作；对于缺失的部分，我做了重新本地构建rpm的操作，具体详情如下：

1、**首先**，基础软件包做了部署和安装过程，对于其中缺失的依赖，且不包含在dnf包管理器中的，我做了重新构建rpm以及安装，详情参考下图：

![daadbd13af996b1bdf3db918559fd31](https://github.com/xiaodouzi666/openEuler-/assets/77219630/aace21b1-410b-4dbf-aff1-e728a115a5a1)

![2ed7d6f84a1d2e0e430069298c3cc1f](https://github.com/xiaodouzi666/openEuler-/assets/77219630/67d9363b-4535-4474-a180-590ab722b73c)

![43378d7968bb7e0eb7bc1736a55855d](https://github.com/xiaodouzi666/openEuler-/assets/77219630/e448e037-5a3b-45b4-9d43-9795e4aa5033)

以上是安装pytorch的rpm时候新增加的一些其他的rpm的依赖以及安装成功的截图，由于在火车上使用Termux调试，故截图可能偏大，敬请谅解。

2、**其次**，当构建好依赖之后，原先在EUR平台上一直由于其CMakeLists一直尝试从GitHub下载安装相关zip包，而且包含哈希校验，直接修改的话太过麻烦，故使用魔法在腾讯云的openEuler服务器上尝试重新构建，并最终成功。期间，修复了由于openEuler包管理器中的libc6不存在，而是glibc的问题：
![image](https://github.com/xiaodouzi666/openEuler-/assets/77219630/3682460b-c154-4dab-8aff-95331eb9dba6)

重新修改Requires: glibc后，构建成功：
![eed9113b272f8706079b45bc1e41af0](https://github.com/xiaodouzi666/openEuler-/assets/77219630/85fe2211-611d-4276-8471-568b4db18a2b)


尝试dnf install，不再报错，成功安装：

![077a4253fffee19f50888b6c97a1cca](https://github.com/xiaodouzi666/openEuler-/assets/77219630/71899bf9-36d4-4f27-a0b9-b5fad0d96e29)

略显遗憾的是，由于没有arm架构的机器，故构建的只有x86_64软件包，后续会想办法尝试通过EUR进行补全。

# 在openEuler 22.03 (LTS-SP2)的服务器上进行部署AI推理应用

在构建好并dnf install好了PyTorch、transformer等rpm包之后，接下来开始部署AI推理应用。

这里我选用了在安装transformer的时候顺便构建的HuggingFace hub等软件包，直接从huggingface hub拉取模型，部分模型选用了Gradio做前端呈现，详情如下：

1、构建了**tts(text-to-speech)** 推理应用，并在运行后能输出对应文字的语音wav文件：
![image](https://github.com/xiaodouzi666/openEuler-/assets/77219630/95462190-2eb0-43ba-a771-5c6dd11e253c)

执行运行，能看到将对应的文字输出成语音文件并能正常播放：
![image](https://github.com/xiaodouzi666/openEuler-/assets/77219630/8c0fa4f8-98bc-4334-a183-8552b98599cc)

后续，将尝试将输入内容改为用户自行输入，并使用Gradio做前端呈现。本次由于时间关系，无法兼顾，后续将会持续开发，并提交PR到社区仓库。

2、构建了**情感分析** AI推理应用，并能在运行后打印输出对应情感语句是正向还是反向的评判，并给出相似度的评分：

![cde57a5d083b92d410fa280cb5707fa](https://github.com/xiaodouzi666/openEuler-/assets/77219630/29d3cb15-b440-47ba-a1e9-8b6f24f8c789)

3、构建了**图片分类** AI推理应用，并使用Gradio实现了前端用户自行上传图片，并实现推理结果显示功能：

![image](https://github.com/xiaodouzi666/openEuler-/assets/77219630/43779e23-8028-4243-abda-2991257fb7dd)

将相关链接放到浏览器中打开，效果如下：

![image](https://github.com/xiaodouzi666/openEuler-/assets/77219630/8369e2a5-3d04-450d-8488-d82597c4711d)

上传相关图片，输出图片对应分类的label，label对应的类别需要去huggingface hub中对应模型仓库中查看映射表。

![image](https://github.com/xiaodouzi666/openEuler-/assets/77219630/adc7d5e5-f541-4449-8fcb-ae6fe5bcb925)

4、构建了**图片风格重绘** AI推理应用，用户上传自己的自拍或其他照片，即可实现风格重绘。代码节选如下：

![image](https://github.com/xiaodouzi666/openEuler-/assets/77219630/c57393a3-97ac-4908-b6eb-55de5f833adb)


# 比赛总结

这次比赛学到了不少东西，特别是rpm包的构建以及spec文件编写，这是以前不具备的技能。另外，相关的pytorch ecosystem软件包，仍有很多原本不存在于openEuler的系统中，后续比赛结束后，如果社区需要，本人可以无偿构建完剩下的全部软件包，社区随时ping我即可：） 
再次感谢openEuler社区，以及开放原子基金会举办的这次比赛。
