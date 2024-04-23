const { ResponseTemplate } = require('../helper/template.helper')
const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()


function TestUser(req, res) {
    let resp = ResponseTemplate(null, 'success', null, 200)
    res.json(resp)
}

async function Insert(req, res) {

    const { room_id, name_student, nrp, major, study_program } = req.body

    const payload = {
        room_id,
        name_student,
        nrp,
        major,
        study_program
    }

    try {
        // Temukan lab
        const form_room = await prisma.room.findUnique({
            where: { id_room: room_id }
        });
        if (!form_room) {
            return res.status(404).json({ error: 'Lab tidak ditemukan.' });
        }
        const room_student = await prisma.room_student.create({
            data: payload
        })

        let resp = ResponseTemplate(room_student, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Get(req, res) {

    const { room_id, name_student, nrp, major, study_program } = req.query

    const payload = {}

    if (room_id) {
        payload.room_id = room_id
    }
    if (name_student) {
        payload.name_student = name_student
    }   
    if (nrp) {
        payload.nrp = nrp
    }
    if (major) {
        payload.major = major
    }      
    if (study_program) {
        payload.study_program = study_program
    }   

    try {
        const page = parseInt(req.query.page) || 1; // Nomor halaman
        const perPage = parseInt(req.query.perPage) || 10; // Jumlah item per halaman
        const skip = (page - 1) * perPage;
        const room_student = await prisma.room_student.findMany({
            skip,
            take: perPage,
            where: payload,                        
        });

        let resp = ResponseTemplate(room_student, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function GetByPK(req, res) {

    const { roomstudentId } = req.params

    try {
        const room_student = await prisma.room_student.findUnique({
            where: {
                id_student: Number(roomstudentId)
            },
            include: {                
                room: true                
            }            
        })

        let resp = ResponseTemplate(room_student, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Update(req, res) {

    const { room_id, name_student, nrp, major, study_program } = req.body
    const { roomstudentId } = req.params

    const payload = {}

    if (!room_id && !name_student && !nrp && !major && !study_program) {
        let resp = ResponseTemplate(null, 'bad request', null, 400)
        res.json(resp)
        return
    }

    if (room_id) {
        payload.room_id = room_id
    }
    if (name_student) {
        payload.name_student = name_student
    }   
    if (nrp) {
        payload.nrp = nrp
    }
    if (major) {
        payload.major = major
    }
    if (study_program) {
        payload.study_program = study_program
    }      


    try {
        const room_student = await prisma.room_student.update({
            where: {
                id_student: Number(roomstudentId)
            },
            data: payload
        })

        let resp = ResponseTemplate(room_student, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Delete(req, res) {

    const { roomstudentId } = req.params

    try {
        const room_student = await prisma.room_student.delete({
            where: {
                id_student: Number(roomstudentId)
            },
        })

        let resp = ResponseTemplate(room_student, 'success', null, 200)
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