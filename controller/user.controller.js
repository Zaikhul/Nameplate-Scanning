const { ResponseTemplate } = require('../helper/template.helper')
const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()


function TestUser(req, res) {
    let resp = ResponseTemplate(null, 'success', null, 200)
    res.json(resp)
}

async function Insert(req, res) {

    const { username, password } = req.body

    const payload = {
        username,
        password
    }

    try {
        const user = await prisma.users.create({
            data: payload
        })

        let resp = ResponseTemplate(user, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Get(req, res) {

    const { username,password } = req.query

    const payload = {}

    if (username) {
        payload.username = username
    }
    if (password) {
        payload.password = password
    }        

    try {
        const page = parseInt(req.query.page) || 1; // Nomor halaman
        const perPage = parseInt(req.query.perPage) || 10; // Jumlah item per halaman
        const skip = (page - 1) * perPage;
        const users = await prisma.users.findMany({
            skip,
            take: perPage,
            where: payload,                  
        });

        let resp = ResponseTemplate(users, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function GetByPK(req, res) {

    const { userId } = req.params

    try {
        const users = await prisma.users.findUnique({
            where: {
                id_user: Number(userId)
            }                        
        })

        let resp = ResponseTemplate(users, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Update(req, res) {

    const { username, password } = req.body
    const { userId } = req.params

    const payload = {}

    if (!username && !password) {
        let resp = ResponseTemplate(null, 'bad request', null, 400)
        res.json(resp)
        return
    }

    if (username) {
        payload.username = username
    }  

    if (password) {
        payload.password = password
    }


    try {
        const user = await prisma.users.update({
            where: {
                id_user: Number(userId)
            },
            data: payload
        })

        let resp = ResponseTemplate(user, 'success', null, 200)
        res.json(resp)
        return

    } catch (error) {
        let resp = ResponseTemplate(null, 'internal server error', error, 500)
        res.json(resp)
        return


    }
}

async function Delete(req, res) {

    const { userId } = req.params

    try {
        const user = await prisma.users.delete({
            where: {
                id_user: Number(userId)
            },
        })

        let resp = ResponseTemplate(user, 'success', null, 200)
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