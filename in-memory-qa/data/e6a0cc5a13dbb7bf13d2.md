---
title: 個人開発しくじり先生 パチプロ支援ツールを作って15日でサービス終了した話
tags: 個人開発 Webサービス リーンスタートアップ パチンコ
author: yuno_miyako
slide: false
---
# 誰も使わないサービスにしないために
私が初めて作ったパンツをシェアするwebアプリは、たったユーザ数4人でサービス終了しました。([個人開発しくじり先生 ユーザ数4人でサービス終了した話](https://qiita.com/yuno_miyako/items/279944fd5ae109924c41))

その時の失敗を以下のように分析しました。

① 友人と盛り上がってその場の**思いつき**で企画してしまった
② **使われるかわからないまま**に作りたいものを作ってしまった
③ 全部の機能が完成するまで**リリースしなかった**

そこで今回は、きちんと上記の３つに対して以下の対策を立て、リーンにプロダクトを作っていきました。

① **バーニングニーズ**を見つけ、自分もしくは顧客が抱える「本当の課題」を解決することを目的にプロダクト開発を行う
② **ユーザインタビュー**をして、買ってくれる顧客が欲しいものを作るためにすり合わせを実施する
③ **MVP**(最もコアの価値がある機能を有したプロダクト)を作ったらそれでリリースしてフィードバックをもらう

# パチプロ支援ツールを作る

## ① バーニングニーズを見つけた
友人にパチンコで月数十万円を稼いで生活をしているパチプロがいたため、単純な興味からどんな風にしてパチンコで稼いでいるのか話を聞いた。
その中で大きなバーニングニーズがあることがわかった。

パチプロは主にデータサイト(パチンコ台が今日どれくらい打たれたかとか、大当たりが何回出たかなどの情報が30分間隔で更新されるサイト)を利用している。毎日夜に**1~2時間程度かけてデータサイトを巡り**、明日稼げそうな台を探している。ここに非常に手間と時間がかかっていた。
これを自動化させることで、1時間/日 × 30日 = 30時間/月の苦痛な時間を削減できる。

## ② ユーザインタビューを繰り返す
パチプロの友人とは何度もミーティングを重ね、美味しい台を見つける計算ロジック(向こうは数学的に考えているわけではなかったりするので、それを数式に落とし込むことは結構大変だった)、表示したい情報、UIのすり合わせを行った。
自分自身もパチンコを打ってみて、こういう仕組みなのかというのを実体験しながらプロダクト像を作っていった。

## ③ MVPを作ってリリース
MVPは1時間かけて回らないと収集できないデータを一瞬で集めて、集計し、翌日どこのお店のどの台を狙うべきか一覧で出ることだったので、その機能を作って2日でリリースした。
最初のMVPは、UIなどない**API**だ。
「このURLを叩くとJSONでスコアの高い台がソートされて一覧が出るから」とパチプロに伝えて使ってもらった。
お金を払ってでも使いたいほどに困っているか確かめるため、**きちんと料金をとった**。(ここをなあなあにすると、別にいらないけど付き合いで使ってあげるというのが生じてしまう)

# なぜ15日でサービス終了したのか

## スクレイピングしているのバレてアカウントを消されたため
データサイトの利用規約にスクレイピング禁止がされているのは当初から認識していたが、そこから目を逸らして実現させてしまった

# しくじりから学んだこと
一発アウトな夜も眠れぬ問題からは目を逸らさないこと。

* 利用規約をちゃんと読む
* 実現可能なのか
* ニーズがあるのか
* セキュリティの問題はないのか
* ビジネスモデルは成り立つのか
* データソースはあるのか

などなど。
あなたのプロジェクトの夜も眠れぬ問題って何ですか？
