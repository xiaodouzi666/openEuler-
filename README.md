# openEuler挑战赛说明文档

接续AtomGit仓库中的内容，这里提出3月份EUR平台炸了之后本地构建的所有操作的内容，以及比赛要求的“在系统上完成对应框架软件包安装部署以及实现推理应用”的实现过程，以及详细说明。

# EUR平台炸了之后的操作
首先，对于已经构建好的软件包，我做了安装部署操作；对于缺失的部分，我做了重新本地构建rpm的操作，具体详情如下：

1、首先，基础软件包做了部署和安装过程，对于其中缺失的依赖，且不包含在dnf包管理器中的，我做了重新构建rpm以及安装，详情参考下图：

![daadbd13af996b1bdf3db918559fd31](https://github.com/xiaodouzi666/openEuler-/assets/77219630/aace21b1-410b-4dbf-aff1-e728a115a5a1)

![2ed7d6f84a1d2e0e430069298c3cc1f](https://github.com/xiaodouzi666/openEuler-/assets/77219630/67d9363b-4535-4474-a180-590ab722b73c)

![43378d7968bb7e0eb7bc1736a55855d](https://github.com/xiaodouzi666/openEuler-/assets/77219630/e448e037-5a3b-45b4-9d43-9795e4aa5033)

以上是安装pytorch的rpm时候新增加的一些其他的rpm的依赖以及安装成功的截图。
