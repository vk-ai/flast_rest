from flask import Blueprint, request, jsonify
from src.contants.http_status_codes import *
from src.database import Bookmark, db
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required

bookmarks = Blueprint("bookmarks", __name__,url_prefix="/api/v1/bookmarks")

@bookmarks.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        body=request.get_json().get('body', '')
        url=request.get_json().get('url', '')
        
        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            }),  HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                'error': 'URL already exists'
            }), HTTP_409_CONFLICT
            
        bookmark=Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()
        
        return jsonify({
            'id':bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visits': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
        })
    else:
        page=request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        
        bookmarks=Bookmark.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)
        data = []
        for bookmark in bookmarks:
            data.append({
                'id':bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at
            })
        meta = {
            "page": bookmarks.page,
            "pages": bookmarks.pages,
            "total_count": bookmarks.total,
            "prev_page": bookmarks.prev_num,
            "next_page": bookmarks.next_num,
            "has_next": bookmarks.has_next,
            "has_prev": bookmarks.has_prev,
        }
        
        return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()
    
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
    
    if not bookmark:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    
    return jsonify({
        'id':bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visits': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), HTTP_200_OK
    
    
@bookmarks.put("/<int:id>")
@bookmarks.patch("/<int:id>")
@jwt_required()
def edit_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
    
    if not bookmark:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    
    body=request.get_json().get('body', '')
    url=request.get_json().get('url', '')
    
    if not validators.url(url):
        return jsonify({
            'error': 'Enter a valid url'
        }),  HTTP_400_BAD_REQUEST
        
    bookmark.url = url
    bookmark.body=body
    
    db.session.add(bookmark)
    db.session.commit()
    
    return jsonify({
        'id':bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visits': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), HTTP_200_OK


@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()
    
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
    
    if not bookmark:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    
    db.session.delete(bookmark)
    db.session.commit()
    
    return jsonify({}), HTTP_204_NO_CONTENT
    