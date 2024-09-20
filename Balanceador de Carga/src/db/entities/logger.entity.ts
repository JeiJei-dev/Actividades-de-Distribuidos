import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";

@Entity()
export class DbLogger {
  @PrimaryGeneratedColumn()
  public id: number;

  @Column()
  public date: Date;

  @Column()
  public port: number;
}
