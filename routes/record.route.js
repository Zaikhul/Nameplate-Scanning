const express = require('express')
const router = express.Router()
const { Get, Insert, GetByPK, Update, Delete } = require('../controller/record.controller')
const { CheckPostRecord } = require('../middleware/middleware')

router.get('/', Get)
router.get('/:recordId', GetByPK)
router.post('/', CheckPostRecord, Insert)
router.put('/:recordId', Update)
router.delete('/:recordId', Delete)
module.exports = router