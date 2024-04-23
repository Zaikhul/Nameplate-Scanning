const { ResponseTemplate } = require('../helper/template.helper')
const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()


function TestUser(req, res) {
    let resp = ResponseTemplate(null, 'success', null, 200)
    res.json(resp)
}

async function Insert(req, res) {

    const { room_id, name_lecture, nim, major } = req.body

    const payload = {}

    if (room_id) {
        payload.room_id = room_id
    }
    if (name_lecture) {
        payload.name_lecture = name_lecture
    }   
    if (nim) {
        payload.nim = nim
    }
    if (major) {
        payload.major = major
    }

    try {
        // Temukan lab
        const form_room = await prisma.room.findUnique({
            where: { id_room: room_id }
        });
        if (!form_room) {
            return res.status(404).json({ error: 'Lab tidak ditemukan.' });
        }
        const room_lecture = await prisma.room_lecture.create({
            data: payload
        })

        let resp = ResponseTemplate(room_lecture, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Get(req, res) {

    const { room_id, name_lecture, nim, major } = req.query

    const payload = {}

    if (room_id) {
        payload.room_id = room_id
    }
    if (name_lecture) {
        payload.name_lecture = name_lecture
    }   
    if (nim) {
        payload.nim = nim
    }
    if (major) {
        payload.major = major
    }         

    try {
        const page = parseInt(req.query.page) || 1; // Nomor halaman
        const perPage = parseInt(req.query.perPage) || 10; // Jumlah item per halaman
        const skip = (page - 1) * perPage;
        const room_lecture = await prisma.room_lecture.findMany({
            skip,
            take: perPage,
            where: payload,                        
        });

        let resp = ResponseTemplate(room_lecture, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function GetByPK(req, res) {

    const { roomLectureId } = req.params

    try {
        const room_lecture = await prisma.room_lecture.findUnique({
            where: {
                id_lecture: Number(roomLectureId)
            },
            include: {                
                room: true                
            }            
        })

        let resp = ResponseTemplate(room_lecture, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Update(req, res) {

    const { room_id, name_lecture, nim, major } = req.body
    const { roomLectureId } = req.params

    const payload = {}

    if (!room_id && !name_lecture && !nim && !major) {
        let resp = ResponseTemplate(null, 'bad request', null, 400)
        res.json(resp)
        return
    }

    if (room_id) {
        payload.room_id = room_id
    }
    if (name_lecture) {
        payload.name_lecture = name_lecture
    }   
    if (nim) {
        payload.nim = nim
    }
    if (major) {
        payload.major = major
    }      


    try {
        const room_lecture = await prisma.room_lecture.update({
            where: {
                id_lecture: Number(roomLectureId)
            },
            data: payload
        })

        let resp = ResponseTemplate(room_lecture, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Delete(req, res) {

    const { roomLectureId } = req.params

    try {
        const room_lecture = await prisma.room_lecture.delete({
            where: {
                id_lecture: Number(roomLectureId)
            },
        })

        let resp = ResponseTemplate(room_lecture, 'success', null, 200)
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