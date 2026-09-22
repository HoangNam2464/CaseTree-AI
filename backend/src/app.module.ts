import { Module } from "@nestjs/common";
import { ConfigModule } from "@nestjs/config";
import { HealthModule } from "./common/health/health.module";
import { AuthModule } from "./modules/auth/auth.module";
import { UserModule } from "./modules/user/user.module";
import { CourseModule } from "./modules/course/course.module";
import { MaterialModule } from "./modules/material/material.module";
import { CaseModule } from "./modules/case/case.module";
import { BranchingAttemptModule } from "./modules/branching-attempt/branching-attempt.module";
import { ReasoningModule } from "./modules/reasoning/reasoning.module";
import { ChallengeSupportModule } from "./modules/challenge-support/challenge-support.module";
import { ReviewStudyModule } from "./modules/review-study/review-study.module";
import { LecturerFeedbackModule } from "./modules/lecturer-feedback/lecturer-feedback.module";
import { StatisticsModule } from "./modules/statistics/statistics.module";
import { NotificationModule } from "./modules/notification/notification.module";
import { EvaluationModule } from "./modules/evaluation/evaluation.module";

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: [".env.local", ".env"],
    }),
    HealthModule,
    AuthModule,
    UserModule,
    CourseModule,
    MaterialModule,
    CaseModule,
    BranchingAttemptModule,
    ReasoningModule,
    ChallengeSupportModule,
    ReviewStudyModule,
    LecturerFeedbackModule,
    StatisticsModule,
    NotificationModule,
    EvaluationModule,
  ],
})
export class AppModule {}
