/*
  Warnings:

  - The primary key for the `users` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `email` on the `users` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `users` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `users` table. All the data in the column will be lost.
  - You are about to drop the `bank_accounts` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `profiles` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `transaction` table. If the table is not empty, all the data it contains will be lost.
  - Added the required column `username` to the `users` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "bank_accounts" DROP CONSTRAINT "bank_accounts_user_id_fkey";

-- DropForeignKey
ALTER TABLE "profiles" DROP CONSTRAINT "profiles_user_id_fkey";

-- DropForeignKey
ALTER TABLE "transaction" DROP CONSTRAINT "transaction_destination_account_id_fkey";

-- DropForeignKey
ALTER TABLE "transaction" DROP CONSTRAINT "transaction_source_account_id_fkey";

-- DropIndex
DROP INDEX "users_email_key";

-- DropIndex
DROP INDEX "users_name_key";

-- AlterTable
ALTER TABLE "users" DROP CONSTRAINT "users_pkey",
DROP COLUMN "email",
DROP COLUMN "id",
DROP COLUMN "name",
ADD COLUMN     "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "id_user" SERIAL NOT NULL,
ADD COLUMN     "username" TEXT NOT NULL,
ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id_user");

-- DropTable
DROP TABLE "bank_accounts";

-- DropTable
DROP TABLE "profiles";

-- DropTable
DROP TABLE "transaction";

-- CreateTable
CREATE TABLE "laboratorium" (
    "id_lab" SERIAL NOT NULL,
    "lab_code" TEXT NOT NULL,
    "position" TEXT NOT NULL,
    "lab_name" TEXT NOT NULL,
    "nama_lab" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "laboratorium_pkey" PRIMARY KEY ("id_lab")
);

-- CreateTable
CREATE TABLE "lab_lecture" (
    "id_lecture" SERIAL NOT NULL,
    "lab_id" INTEGER NOT NULL,
    "name_lecture" TEXT NOT NULL,
    "nim" INTEGER NOT NULL,
    "major" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "lab_lecture_pkey" PRIMARY KEY ("id_lecture")
);

-- CreateTable
CREATE TABLE "lab_information" (
    "id_inform" SERIAL NOT NULL,
    "lab_id" INTEGER NOT NULL,
    "lab_head" INTEGER NOT NULL,
    "laboratorium_field" TEXT NOT NULL,
    "information_lab" TEXT NOT NULL,
    "research_list" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "lab_information_pkey" PRIMARY KEY ("id_inform")
);

-- CreateTable
CREATE TABLE "lab_student" (
    "id_student" SERIAL NOT NULL,
    "lab_id" INTEGER NOT NULL,
    "name_student" TEXT NOT NULL,
    "nrp" INTEGER NOT NULL,
    "major" TEXT NOT NULL,
    "study_program" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "lab_student_pkey" PRIMARY KEY ("id_student")
);

-- CreateIndex
CREATE UNIQUE INDEX "laboratorium_lab_code_key" ON "laboratorium"("lab_code");

-- CreateIndex
CREATE UNIQUE INDEX "lab_lecture_lab_id_key" ON "lab_lecture"("lab_id");

-- CreateIndex
CREATE UNIQUE INDEX "lab_information_lab_id_key" ON "lab_information"("lab_id");

-- CreateIndex
CREATE UNIQUE INDEX "lab_information_lab_head_key" ON "lab_information"("lab_head");

-- CreateIndex
CREATE UNIQUE INDEX "lab_student_lab_id_key" ON "lab_student"("lab_id");

-- AddForeignKey
ALTER TABLE "lab_lecture" ADD CONSTRAINT "lab_lecture_lab_id_fkey" FOREIGN KEY ("lab_id") REFERENCES "laboratorium"("id_lab") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lab_information" ADD CONSTRAINT "lab_information_lab_id_fkey" FOREIGN KEY ("lab_id") REFERENCES "laboratorium"("id_lab") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lab_information" ADD CONSTRAINT "lab_information_lab_head_fkey" FOREIGN KEY ("lab_head") REFERENCES "lab_lecture"("id_lecture") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lab_student" ADD CONSTRAINT "lab_student_lab_id_fkey" FOREIGN KEY ("lab_id") REFERENCES "laboratorium"("id_lab") ON DELETE RESTRICT ON UPDATE CASCADE;
