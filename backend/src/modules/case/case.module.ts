import { Module } from "@nestjs/common";
import { CaseController } from "./case.controller";

@Module({
  controllers: [CaseController],
  providers: [],
  exports: [],
})
export class CaseModule {}
