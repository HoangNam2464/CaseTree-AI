import { Module } from "@nestjs/common";
import { CourseController } from "./course.controller";

@Module({
  controllers: [CourseController],
  providers: [],
  exports: [],
})
export class CourseModule {}
