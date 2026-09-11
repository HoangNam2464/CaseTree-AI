import { Module } from "@nestjs/common";
import { StatisticsController } from "./statistics.controller";

@Module({
  controllers: [StatisticsController],
  providers: [],
  exports: [],
})
export class StatisticsModule {}
