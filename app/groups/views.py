# app/home/views.py

from flask import render_template, request, redirect, session
from app import db
from . import groups
from app.models import Group, Neighbor, NeighborGroup
from sqlalchemy import text
from flask import jsonify, request


@groups.route('/<member_id>', methods=['GET'])
def my_groups(member_id):
    groups = Group.query.all()
    return jsonify(groups)

@groups.route('/create', methods=['POST'])
def create_group():
    data = request.get_json()
    name = data['name']
    msisdn = data['msisdn']
    nb = Neighbor.query.filter(Neighbor.msisdn == msisdn).first()
    res = {
        'status': -1,
        'message': "Creator of this group is not registered or active!"
    }
    if nb is None:
        return jsonify(res)
    m = Group(name=data['name'], created_by=nb.id)
    db.session.add(m)
    db.session.commit()

    nbgrp = NeighborGroup(group_id=m.id, neighbor_id=m.created_by)
    db.session.add(nbgrp)
    db.session.commit()
    return jsonify({'status': 0, 'message': 'Successfully created group', 'id': m.id})


@groups.route('/members/add', methods=['POST'])
def add_members():
    group_id = data['group_id']
    data = request.get_json()
    m = Group.query.get(group_id)
    res = {
        'status': -1,
        'message': "Group not found: {}".format(group_id)
    }
    if m is None:
        return jsonify(res)

    members = data['members']
    for mb in members:
        nb = Neighbor.query.filter(Neighbor.msisdn == mb.msisdn).first()
        if nb is None:
            nb = Neighbor(name=mb.name, msisdn=mb.msisdn, status=1)
            db.session.add(nb)
            db.session.commit()
        nbgrp = NeighborGroup(group_id=group_id, neighbor_id=nb.id)
        db.session.add(nbgrp)
    db.session.commit()
    return jsonify({'result': 0, 'message': 'Successfully added new members to a group'})
