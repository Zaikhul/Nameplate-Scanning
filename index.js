const express = require('express')
const app = express()
const router = require('./routes/route')
const multer = require('multer');
const path = require('path');
const { performOcr } = require('./ocr'); // asumsikan Anda memiliki modul ini

require('dotenv').config()

const port = process.env.PORT || 3000

// Konfigurasi multer untuk menangani upload gambar
const storage = multer.diskStorage({
  destination: './uploads',
  filename: function(req, file, cb){
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  limits:{fileSize: 1000000},
}).single('myImage');

app.post('/upload', (req, res) => {
  upload(req, res, (err) => {
    if(err){
      res.json({message: err});
    } else {
      if(req.file == undefined){
        res.json({message: 'Error: No File Selected!'});
      } else {
        performOcr(req.file.path).then(ocrResult => {
          res.json({message: 'Image Uploaded!', ocrResult});
        });
      }
    }
  });
});

app.use(express.json())
app.use(express.urlencoded({ extended: false }))

app.set('view engine', 'ejs')
app.use('/', router)

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})
