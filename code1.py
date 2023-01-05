import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
# api_key
# 프로그램이 서버와 통신할 수 있도록 해주는 것
tmdb.api_key = 'f4010c68a18cda1b1f83565347668b17'
tmdb.language = 'ko-KR'

def get_recommendations(title):
  # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값 얻기
  idx = movies[movies['title'] == title].index[0]

  # 코사인 유사도 매트릭스에서 idx에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
  sim_scores = list(enumerate(cosine_sim[idx]))

  # 코사인 유사도 기준으로 내림차순 정렬
  sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
  
  # 자기자신을 제외한 영화 10개 추천받기
  sim_scores = sim_scores[1:11]

  # 추천 영화 목록 10개의 인덱스 정보 추출
  movie_indices = [i[0] for i in sim_scores]

  # 인덱스 정보를 통해 영화 제목 추출
  images = []
  titles = []
  for i in movie_indices:
    id = movies['id'].iloc[i]
    details = movie.details(id) # tmdb api 가 가지고 있는 여러 정보가 있다

    image_path = details['poster_path']
    if image_path:
        image_path = 'https://image.tmdb.org/t/p/w500/' + image_path
    else:
        image_path = 'no_image.jpg'

    images.append(image_path)
    titles.append(details['title'])

  return images, titles



movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout='wide') # 전체화면 설정
# 헤더 설정
st.header('Nadoflix')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)

# 추천 버튼 만들기
if st.button('Recommend'):
    with st.spinner('Please wait...'):
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0, 2):
            cols = st.columns(5) # 컬럼 만들어준다
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1
