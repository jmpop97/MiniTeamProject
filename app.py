from flask import Flask, render_template, request, jsonify
from bson import json_util
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.vnhcwoi.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

# 메인 페이지
@app.route('/')
def main():
    return render_template('matgo.html')

# 테스트 시작하기
@app.route('/matgo')
def matgo():
    return render_template('matgo.html')

# 맛집 조회 + 디테일 들어가기
@app.route("/matgo/matjips", methods=["GET"])
def matgo_get():
    # 여러개 찾기 - 예시 ( _id 값은 제외하고 출력)
    # all_matjips = list(db.matjip.find({},{'_id':False}))
    all_matjips = list(db.matjip.find({}))
    # all_matjips = list(db.matjip.find(  {}
                                        # {
                                            # str(result.get('_id'))
                                            # ObjectId idObj = (ObjectId)obj.get("_id");
                                            # String _id = idObj.toString()
                                        # }
                                    #)
                        #)
    # all_matjips = list(db.matjip.find(
    #     {},{
    #         '_id': str(objectIdDecoder({"_id": ObjectId(id)}))
    #     }
    #))
    # return jsonify({'result': all_matjips})  # render_template와 jsonify의 차이...
    return json_util.dumps({'result': all_matjips})
    # return render_template({'result': all_matjips})
    # return json.dumps({'result': all_matjips})
# objectId 찾기
def objectIdDecoder(list):
  results=[]
  for document in list:
    document['_id'] = str(document['_id'])
    results.append(document)
  return results


@app.route('/write')
def write():
    return render_template('write.html')

@app.route("/write", methods=["POST"])
def matjip_post():
    url_receive = request.form['url_give']
    #가게이름
    stname_receive = request.form['stname_give']
    #가게소개
    stintro_receive = request.form['stintro_give']
    #주소 추후 주소API, 카카오맵API
    stadd_receive = request.form['stadd_give']

    ststar_receive = request.form['ststar_give']
    comment_receive = request.form['comment_give']
    #평균 가격이 아니라 가격
    price_receive = request.form['price_give']

    # headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(url_receive,headers=headers)

    # soup = BeautifulSoup(data.text, 'html.parser')

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.
    # ogimage = soup.select_one('meta[property="og:image"]')['content']
    
    doc = {
        'url': url_receive,
        'stname': stname_receive,
        'stintro': stintro_receive,
        'stadd': stadd_receive,
        'ststar': ststar_receive,
        'comment': comment_receive,
        'price': price_receive        
    }

    # 저장
    db.matjip.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

@app.route('/matgo_list_detail/<id>')
def matgo_list_detail(id):

    return render_template('matgo_list_detail.html',Resid=id)

@app.route('/matgo_list_detail/<id>', methods=["GET"])
def matgo_list_detail_get(id):
    all_matjips = db.matjip.find({'_id'(id)})
    return jsonify({'result': all_matjips})

@app.route('/matgo_list_detail/<id>', methods=["POST"])
def matgo_list_detail_post(id):
    id_receive=id
    star_receive = request.form['reviewstar_give']
    review_receive = request.form['review_comment_give']
    doc={
        'Res_id':id_receive,
        'Res_star': star_receive,
        'Res_review': review_receive
    }
    db.Resinfo.insert_one(doc)
    return jsonify({'msg':'저장완료!'})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)