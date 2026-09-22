import { Module } from "@nestjs/common";
import { LecturerFeedbackController } from "./lecturer-feedback.controller";

@Module({
  controllers: [LecturerFeedbackController],
  providers: [],
  exports: [],
})
export class LecturerFeedbackModule {}
