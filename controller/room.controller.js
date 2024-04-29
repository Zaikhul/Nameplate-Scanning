const { ResponseTemplate } = require('../helper/template.helper')
const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()


function TestUser(req, res) {
    let resp = ResponseTemplate(null, 'success', null, 200)
    res.json(resp)
}

async function Insert(req, res) {

    const { room_code, position, room_name, nama_ruangan } = req.body

    const payload = {
        room_code,
        position,
        room_name,
        nama_ruangan
    }

    try {
        const room = await prisma.room.create({
            data: payload
        })

        let resp = ResponseTemplate(room, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Get(req, res) {

    const { room_code, position, room_name, nama_ruangan } = req.query

    const payload = {}

    if (room_code) {
        payload.room_code = room_code
    }
    if (position) {
        payload.position = position
    }   
    if (room_name) {
        payload.room_name = room_name
    }
    if (nama_ruangan) {
        payload.nama_ruangan = nama_ruangan
    }     

    try {
        const page = parseInt(req.query.page) || 1; // Nomor halaman
        const perPage = parseInt(req.query.perPage) || 10; // Jumlah item per halaman
        const skip = (page - 1) * perPage;
        const room = await prisma.room.findMany({
            skip,
            take: perPage,
            where: payload,                        
        });

        let resp = ResponseTemplate(room, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function GetByPK(req, res) {

    const { roomId } = req.params

    try {
        const room = await prisma.room.findUnique({
            where: {
                id_room: Number(roomId)
            },
            include: {                
                room_informations: true,                
                room_students: true,                
                room_lectures: true,                
            }             
        })

        let resp = ResponseTemplate(room, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function GetRoomCode(req, res) {

    const { roomCode } = req.params

    try {
        const room = await prisma.room.findMany({
            where: {
                room_code: roomCode
            },
            include: {                
                room_informations: true,                
                room_students: true,                
                room_lectures: true,                
            }             
        })

        let resp = ResponseTemplate(room, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function GetRoomName(req, res) {

    const { roomName } = req.params

    try {
        const room = await prisma.room.findMany({
            where: {
                room_name: roomName
            },
            include: {                
                room_informations: true,                
                room_students: true,                
                room_lectures: true,                
            }             
        })

        let resp = ResponseTemplate(room, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function GetRoomNama(req, res) {

    const { roomNama } = req.params

    try {
        const room = await prisma.room.findMany({
            where: {
                nama_ruangan: roomNama
            },
            include: {                
                room_informations: true,                
                room_students: true,                
                room_lectures: true,                
            }             
        })

        let resp = ResponseTemplate(room, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function coba(req, res) {

    //const { roomId } = req.params

    try {
        const room = await prisma.room.findMany({
            where: {
                room_code: "0705"
            },
            select: {
                room_name: true,
                position: true,                
                nama_ruangan: true,
            },             
        })

        let resp = ResponseTemplate(room, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Update(req, res) {

    const { room_code, position, room_name, nama_ruangan } = req.body
    const { roomId } = req.params

    const payload = {}

    if (!room_code && !position && !room_name && !nama_ruangan) {
        let resp = ResponseTemplate(null, 'bad request', null, 400)
        res.json(resp)
        return
    }

    if (room_code) {
        payload.room_code = room_code
    }
    if (position) {
        payload.position = position
    }   
    if (room_name) {
        payload.room_name = room_name
    }
    if (nama_ruangan) {
        payload.nama_ruangan = nama_ruangan
    }      


    try {
        const room = await prisma.room.update({
            where: {
                id_room: Number(roomId)
            },
            data: payload
        })

        let resp = ResponseTemplate(room, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Delete(req, res) {

    const { roomId } = req.params

    try {
        const room = await prisma.room.delete({
            where: {
                id_room: Number(roomId)
            },
        })

        let resp = ResponseTemplate(room, 'success', null, 200)
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
    Delete,
    GetRoomCode,
    GetRoomName,
    GetRoomNama,
    coba
}