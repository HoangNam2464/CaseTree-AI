import { Module } from "@nestjs/common";
import { ReviewStudyController } from "./review-study.controller";

@Module({
  controllers: [ReviewStudyController],
  providers: [],
  exports: [],
})
export class ReviewStudyModule {}
