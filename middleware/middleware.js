
const { ResponseTemplate } = require('../helper/template.helper')
const Joi = require('joi');
// function PrintSuccess(req, res, next) {
//     const { } = req.params.id
//     console.log(` SELALU BERHASIL AKSES`)
//     next()
// }

// function PrintSuccessRoute(req, res, next) {

//     console.log(` SELALU BERHASIL AKSES LEWAT ROUTE LEVEL`)
//     next()
// }

function CheckPostReq(req, res, next) {
    const schema = Joi.object({
        username: Joi.string().alphanum().max(255).required(),
        password: Joi.string().alphanum().required(),        
    })

    const { error } = schema.validate(req.body)
    if (error) {
        let respErr = ResponseTemplate(null, 'invalid request',
            error.details[0].message, 400)
        res.json(respErr)
        return
    }

    next()
}

function CheckPostRecord(req, res, next) {
    const schema = Joi.object({
        room_code: Joi.string().max(255).required(),                        
    })

    const { error } = schema.validate(req.body)
    if (error) {
        let respErr = ResponseTemplate(null, 'invalid request',
            error.details[0].message, 400)
        res.json(respErr)
        return
    }

    next()
}

function CheckPostRoom(req, res, next) {
    const schema = Joi.object({
        room_code: Joi.string().max(255).required(),
        position: Joi.string().required(),        
        room_name: Joi.string().required(),        
        nama_ruangan: Joi.string().required(),                
    })

    const { error } = schema.validate(req.body)
    if (error) {
        let respErr = ResponseTemplate(null, 'invalid request',
            error.details[0].message, 400)
        res.json(respErr)
        return
    }

    next()
}

function CheckPostRoomInform(req, res, next) {
    const schema = Joi.object({
        room_id: Joi.number().required(),
        room_head: Joi.number().required(),
        room_type: Joi.string().required(),
        information_room: Joi.string().required(),        
        research_list: Joi.string().required(),                
    })

    const { error } = schema.validate(req.body)
    if (error) {
        let respErr = ResponseTemplate(null, 'invalid request',
            error.details[0].message, 400)
        res.json(respErr)
        return
    }

    next()
}

function CheckPostRoomLecture(req, res, next) {
    const schema = Joi.object({
        room_id: Joi.number().required(),        
        name_lecture: Joi.string().alphanum().required(),
        nim: Joi.number().required(),
        major: Joi.string().alphanum().required(),                
    })

    const { error } = schema.validate(req.body)
    if (error) {
        let respErr = ResponseTemplate(null, 'invalid request',
            error.details[0].message, 400)
        res.json(respErr)
        return
    }

    next()
}

function CheckPostRoomStudent(req, res, next) {
    const schema = Joi.object({
        room_id: Joi.number().required(),        
        name_student: Joi.string().alphanum().required(),
        nrp: Joi.number().required(),
        major: Joi.string().alphanum().required(),                
        study_program: Joi.string().alphanum().required(),        
    })

    const { error } = schema.validate(req.body)
    if (error) {
        let respErr = ResponseTemplate(null, 'invalid request',
            error.details[0].message, 400)
        res.json(respErr)
        return
    }

    next()
}


module.exports = {
    CheckPostReq,
    CheckPostRoom,
    CheckPostRoomInform,
    CheckPostRoomLecture,
    CheckPostRoomStudent,
    CheckPostRecord    
}