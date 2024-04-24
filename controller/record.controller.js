const { ResponseTemplate } = require('../helper/template.helper')
const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()


function TestUser(req, res) {
    let resp = ResponseTemplate(null, 'success', null, 200)
    res.json(resp)
}

async function Insert(req, res) {

    const { room_code } = req.body

    const payload = {
        room_code        
    }

    try {
        const record = await prisma.record.create({
            data: payload
        })

        let resp = ResponseTemplate(record, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Get(req, res) {

    const { room_code} = req.query

    const payload = {}

    if (room_code) {
        payload.room_code = room_code
    }
       

    try {
        const page = parseInt(req.query.page) || 1; // Nomor halaman
        const perPage = parseInt(req.query.perPage) || 10; // Jumlah item per halaman
        const skip = (page - 1) * perPage;
        const record = await prisma.record.findMany({
            skip,
            take: perPage,
            where: payload,                        
        });

        let resp = ResponseTemplate(record, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function GetByPK(req, res) {

    const { recordId } = req.params

    try {
        const record = await prisma.record.findUnique({
            where: {
                id_record: Number(recordId)
            }             
        })

        let resp = ResponseTemplate(record, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Update(req, res) {

    const { room_code} = req.body
    const { recordId } = req.params

    const payload = {}

    if (!room_code) {
        let resp = ResponseTemplate(null, 'bad request', null, 400)
        res.json(resp)
        return
    }

    if (room_code) {
        payload.room_code = room_code
    }


    try {
        const record = await prisma.record.update({
            where: {
                id_record: Number(recordId)
            },
            data: payload
        })

        let resp = ResponseTemplate(record, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Delete(req, res) {

    const { recordId } = req.params

    try {
        const record = await prisma.record.delete({
            where: {
                id_record: Number(recordId)
            },
        })

        let resp = ResponseTemplate(record, 'success', null, 200)
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