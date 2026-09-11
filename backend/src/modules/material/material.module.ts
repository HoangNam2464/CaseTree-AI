import { Module } from "@nestjs/common";
import { MaterialController } from "./material.controller";

@Module({
  controllers: [MaterialController],
  providers: [],
  exports: [],
})
export class MaterialModule {}
