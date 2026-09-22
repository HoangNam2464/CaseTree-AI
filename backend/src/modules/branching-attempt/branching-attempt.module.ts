import { Module } from "@nestjs/common";
import { BranchingAttemptController } from "./branching-attempt.controller";

@Module({
  controllers: [BranchingAttemptController],
  providers: [],
  exports: [],
})
export class BranchingAttemptModule {}
