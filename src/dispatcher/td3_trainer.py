import numpy as np
import torch
from ml.env import Env
from ml.td3 import TD3
from ml.replay_buffer import ReplayBuffer
from configs.parser import Parser
from assists.prepare_data import PrepareData
from assists.printer import Printer
from strategies.strategies import Strategy
from configs import configs


class TD3Trainer:
    @staticmethod
    def start():
        # parse configs
        train_configs = Parser.parse_train_configs()

        # check data
        if (not PrepareData.check_data(train_configs.data_path)) or train_configs.force_select_data:
            Printer.print_warn(
                "data file not exist or force to regenerate selected data")
            Printer.print_step(0.1, "reading all data...")
            data, header = PrepareData.read_data(
                configs.DATA_PATH_XLSX, header=True)
            Printer.print_step(0.2, "selecting data...")
            selected_indexes = Strategy.select_data(data)
            Printer.print_step(0.3, "writing selected data...")
            data = PrepareData.write_selected_data(
                train_configs.data_path, data, header, selected_indexes)
        else:
            Printer.print_step(0, "reading selected data...")
            data = PrepareData.read_selected_data(train_configs.data_path)

        Printer.print_other(
            "read data finished! get data with shape: %s" % (data.shape,))

        for i in range(len(data)):
            # create env and make dirs
            Printer.print_step(i+1+0.1, "creating env...")
            env = Env.make(train_configs.env_name,
                           data[i][:train_configs.train_test_split])
            eval_env = Env.make(train_configs.env_name,
                                data[i][train_configs.train_test_split:])
            PrepareData.mkdir(train_configs.model_path+str(i)+"/")
            PrepareData.mkdir(train_configs.result_path+str(i)+"/")

            # set seeds
            Printer.print_step(i+1+0.2, "setting seeds...")
            env.set_seed(train_configs.seed)
            torch.manual_seed(train_configs.seed)
            np.random.seed(train_configs.seed)

            # create policy
            Printer.print_step(i+1+0.3, "creating policy...")
            state_dim = env.get_state_dim()
            action_dim = env.get_action_dim()
            max_action = float(env.get_max_action())
            kwargs = {
                "state_dim": state_dim,
                "action_dim": action_dim,
                "max_action": max_action,
                "discount": train_configs.discount,
                "tau": train_configs.tau,
                "policy_noise": train_configs.policy_noise * max_action,
                "noise_clip": train_configs.noise_clip * max_action,
                "policy_freq": train_configs.policy_freq
            }
            policy = TD3(**kwargs)
            if train_configs.load_model:
                policy.load(train_configs.model_path+str(i) +
                            "/"+train_configs.file_name)
            replay_buffer = ReplayBuffer(state_dim, action_dim)

            # start training
            Printer.print_step(i+1+0.4, "training...")
            # evaluate untrained policy and init some variables
            evaluations = [eval_env.eval_policy(policy)[0]]
            state, done = env.reset(), False
            episode_reward = 0
            episode_timesteps = 0
            episode_num = 0
            for t in range(int(train_configs.max_timesteps)):
                episode_timesteps += 1
                # select action randomly or according to policy
                if t < train_configs.start_timesteps:
                    action = env.sample_action()
                else:
                    action = (
                        policy.select_action(np.array(state))
                        + np.random.normal(0, max_action *
                                           train_configs.expl_noise, size=action_dim)
                    ).clip(-max_action, max_action)
                # perform action
                next_state, reward, done = env.step(action)
                # store data in replay buffer
                replay_buffer.add(state, action, next_state, reward, done)
                state = next_state
                episode_reward += reward
                # train agent after collecting sufficient data
                if t >= train_configs.start_timesteps:
                    policy.train(replay_buffer, train_configs.batch_size)

                if done:
                    # +1 to account for 0 indexing. +0 on ep_timesteps since it will increment +1 even if done=True
                    Printer.print_train(
                        f"total T: {t+1} Episode Num: {episode_num+1} Episode T: {episode_timesteps} Reward: {episode_reward:.3f}")
                    # reset environment
                    state, done = env.reset(), False
                    episode_reward = 0
                    episode_timesteps = 0
                    episode_num += 1

                # evaluate episode
                if (t + 1) % train_configs.eval_freq == 0:
                    evaluations.append(eval_env.eval_policy(policy)[0])
                    np.save(train_configs.result_path+str(i)+"/" +
                            train_configs.file_name, evaluations)
                    if train_configs.save_model:
                        policy.save(train_configs.model_path +
                                    str(i)+"/" + train_configs.file_name)

        Printer.print_other("finished!")
