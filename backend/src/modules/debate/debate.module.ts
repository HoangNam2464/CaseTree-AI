import { Module } from "@nestjs/common";
import { DebateController } from "./debate.controller";

@Module({
  controllers: [DebateController],
  providers: [],
  exports: [],
})
export class DebateModule {}
