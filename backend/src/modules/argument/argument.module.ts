import { Module } from "@nestjs/common";
import { ArgumentController } from "./argument.controller";

@Module({
  controllers: [ArgumentController],
  providers: [],
  exports: [],
})
export class ArgumentModule {}
