# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import pandas as pd

recommendation_df = pd.read_json('./data/song_id2playlist_word2vec.json', typ = 'frame')
song_meta_df = pd.read_json('./data/song_meta_data_v3.json', typ = 'frame')

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        song = request.form['song_name']
        song_id = int(song_meta_df[song_meta_df['song_name'] == song]["id"].iloc[0]) # 일단 중복 제목 노래는 첫번째 노래만 가져오도록 함 (자동완성 적용 후 수정 필요)
        song_list = list(recommendation_df[song_id])
        result = []
        for i in range(len(song_list)):
            result.append(song_meta_df[song_meta_df['id']==song_list[i]]["song_name"].values[0])

        return render_template('index.html', output_song_list=result)

if __name__ == '__main__':
   app.run(debug = True)