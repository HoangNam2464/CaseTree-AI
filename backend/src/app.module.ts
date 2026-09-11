import { Module } from "@nestjs/common";
import { ConfigModule } from "@nestjs/config";
import { HealthModule } from "./common/health/health.module";
import { AuthModule } from "./modules/auth/auth.module";
import { UserModule } from "./modules/user/user.module";
import { CourseModule } from "./modules/course/course.module";
import { MaterialModule } from "./modules/material/material.module";
import { CaseModule } from "./modules/case/case.module";
import { SimulationModule } from "./modules/simulation/simulation.module";
import { ArgumentModule } from "./modules/argument/argument.module";
import { DebateModule } from "./modules/debate/debate.module";
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
    SimulationModule,
    ArgumentModule,
    DebateModule,
    StatisticsModule,
    NotificationModule,
    EvaluationModule,
  ],
})
export class AppModule {}
