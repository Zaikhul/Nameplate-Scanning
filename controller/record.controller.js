const { ResponseTemplate } = require('../helper/template.helper')
const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()


function TestUser(req, res) {
    let resp = ResponseTemplate(null, 'success', null, 200)
    res.json(resp)
}

async function Insert(req, res) {

    const { room_id, room_head, room_type, information_room, research_list } = req.body

    const payload = {
        room_id,
        room_head,
        room_type,
        information_room,
        research_list
    }

    try {
        const room_information = await prisma.room_information.create({
            data: payload
        })

        let resp = ResponseTemplate(room_information, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Get(req, res) {

    const { room_id, room_head, room_type, information_room, research_list } = req.query

    const payload = {}

    if (room_id) {
        payload.room_id = room_id
    }
    if (room_head) {
        payload.room_head = room_head
    }   
    if (room_type) {
        payload.room_type = room_type
    }
    if (information_room) {
        payload.information_room = information_room
    }     
    if (research_list) {
        payload.research_list = research_list
    }     

    try {
        const page = parseInt(req.query.page) || 1; // Nomor halaman
        const perPage = parseInt(req.query.perPage) || 10; // Jumlah item per halaman
        const skip = (page - 1) * perPage;
        const room_information = await prisma.room_information.findMany({
            skip,
            take: perPage,
            where: payload,                        
        });

        let resp = ResponseTemplate(room_information, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function GetByPK(req, res) {

    const { roomInformId } = req.params

    try {
        const room_information = await prisma.room_information.findUnique({
            where: {
                id_inform: Number(roomInformId)
            },
            include: {
                room: true,
                room_lecture: true                
            }            
        })

        let resp = ResponseTemplate(room_information, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Update(req, res) {

    const { room_id, room_head, room_type, information_room, research_list } = req.body
    const { roomInformId } = req.params

    const payload = {}

    if (!room_id && !room_head && !room_type && !information_room && !research_list) {
        let resp = ResponseTemplate(null, 'bad request', null, 400)
        res.json(resp)
        return
    }

    if (room_id) {
        payload.room_id = room_id
    }
    if (room_head) {
        payload.room_head = room_head
    }   
    if (room_type) {
        payload.room_type = room_type
    }
    if (information_room) {
        payload.information_room = information_room
    }     
    if (research_list) {
        payload.research_list = research_list
    }      


    try {
        const room_information = await prisma.room_information.update({
            where: {
                id_inform: Number(roomInformId)
            },
            data: payload
        })

        let resp = ResponseTemplate(room_information, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Delete(req, res) {

    const { roomInformId } = req.params

    try {
        const room_information = await prisma.room_information.delete({
            where: {
                id_inform: Number(roomInformId)
            },
        })

        let resp = ResponseTemplate(room_information, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return
    }
}






module.exports = {
    TestUser,
    Insert,
    Get,
    GetByPK,
    Update,
    Delete
}