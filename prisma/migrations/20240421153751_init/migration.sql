/*
  Warnings:

  - You are about to drop the column `createdAt` on the `users` table. All the data in the column will be lost.
  - You are about to drop the `lab_information` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `lab_lecture` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `lab_student` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `laboratorium` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "lab_information" DROP CONSTRAINT "lab_information_lab_head_fkey";

-- DropForeignKey
ALTER TABLE "lab_information" DROP CONSTRAINT "lab_information_lab_id_fkey";

-- DropForeignKey
ALTER TABLE "lab_lecture" DROP CONSTRAINT "lab_lecture_lab_id_fkey";

-- DropForeignKey
ALTER TABLE "lab_student" DROP CONSTRAINT "lab_student_lab_id_fkey";

-- AlterTable
ALTER TABLE "users" DROP COLUMN "createdAt",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- DropTable
DROP TABLE "lab_information";

-- DropTable
DROP TABLE "lab_lecture";

-- DropTable
DROP TABLE "lab_student";

-- DropTable
DROP TABLE "laboratorium";

-- CreateTable
CREATE TABLE "record" (
    "id_record" SERIAL NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "record_pkey" PRIMARY KEY ("id_record")
);

-- CreateTable
CREATE TABLE "room" (
    "id_room" SERIAL NOT NULL,
    "room_code" TEXT NOT NULL,
    "position" TEXT NOT NULL,
    "room_name" TEXT NOT NULL,
    "nama_ruangan" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "room_pkey" PRIMARY KEY ("id_room")
);

-- CreateTable
CREATE TABLE "room_lecture" (
    "id_lecture" SERIAL NOT NULL,
    "room_id" INTEGER NOT NULL,
    "name_lecture" TEXT NOT NULL,
    "nim" INTEGER NOT NULL,
    "major" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "room_lecture_pkey" PRIMARY KEY ("id_lecture")
);

-- CreateTable
CREATE TABLE "room_information" (
    "id_inform" SERIAL NOT NULL,
    "room_id" INTEGER NOT NULL,
    "room_head" INTEGER NOT NULL,
    "room_type" TEXT NOT NULL,
    "information_room" TEXT NOT NULL,
    "research_list" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "room_information_pkey" PRIMARY KEY ("id_inform")
);

-- CreateTable
CREATE TABLE "room_student" (
    "id_student" SERIAL NOT NULL,
    "room_id" INTEGER NOT NULL,
    "name_student" TEXT NOT NULL,
    "nrp" INTEGER NOT NULL,
    "major" TEXT NOT NULL,
    "study_program" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "room_student_pkey" PRIMARY KEY ("id_student")
);

-- CreateIndex
CREATE UNIQUE INDEX "room_lecture_room_id_key" ON "room_lecture"("room_id");

-- CreateIndex
CREATE UNIQUE INDEX "room_information_room_id_key" ON "room_information"("room_id");

-- CreateIndex
CREATE UNIQUE INDEX "room_information_room_head_key" ON "room_information"("room_head");

-- CreateIndex
CREATE UNIQUE INDEX "room_student_room_id_key" ON "room_student"("room_id");

-- AddForeignKey
ALTER TABLE "room_lecture" ADD CONSTRAINT "room_lecture_room_id_fkey" FOREIGN KEY ("room_id") REFERENCES "room"("id_room") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "room_information" ADD CONSTRAINT "room_information_room_id_fkey" FOREIGN KEY ("room_id") REFERENCES "room"("id_room") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "room_information" ADD CONSTRAINT "room_information_room_head_fkey" FOREIGN KEY ("room_head") REFERENCES "room_lecture"("id_lecture") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "room_student" ADD CONSTRAINT "room_student_room_id_fkey" FOREIGN KEY ("room_id") REFERENCES "room"("id_room") ON DELETE RESTRICT ON UPDATE CASCADE;
