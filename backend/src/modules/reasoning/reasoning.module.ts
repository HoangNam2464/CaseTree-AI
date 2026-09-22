import { Module } from "@nestjs/common";
import { ReasoningController } from "./reasoning.controller";

@Module({
  controllers: [ReasoningController],
  providers: [],
  exports: [],
})
export class ReasoningModule {}
