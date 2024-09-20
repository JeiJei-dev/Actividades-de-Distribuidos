import { Injectable, Logger } from "@nestjs/common";
import { InjectEntityManager } from "@nestjs/typeorm";
import { EntityManager } from "typeorm";
import { DbLogger } from "./db/entities/logger.entity";
import { extractServicePort } from "./utils/extract-service-port.util";

@Injectable()
export class AppService {
  private logger: Logger;
  constructor(@InjectEntityManager() private entityManager: EntityManager) {
    this.logger = new Logger(AppService.name);
  }

  async setNewConnection() {
    this.logger.log("New connection established");
    const port = await extractServicePort("logger-port");
    this.logger.log(port);
    const connection = await this.entityManager.getRepository(DbLogger).save({
      date: new Date(),
      port,
    });
    return connection;
  }

  async getUsers() {
    this.logger.log("Getting connections");
    return await this.entityManager.getRepository(DbLogger).find();
  }
}
