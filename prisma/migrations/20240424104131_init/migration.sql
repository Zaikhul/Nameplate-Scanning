/*
  Warnings:

  - Added the required column `room_code` to the `record` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "record" ADD COLUMN     "room_code" TEXT NOT NULL;
