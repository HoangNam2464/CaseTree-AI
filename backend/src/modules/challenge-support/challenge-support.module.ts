import { Module } from "@nestjs/common";
import { ChallengeSupportController } from "./challenge-support.controller";

@Module({
  controllers: [ChallengeSupportController],
  providers: [],
  exports: [],
})
export class ChallengeSupportModule {}
