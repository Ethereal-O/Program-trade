import numpy as np
import torch
from ml.env import Env
from ml.td3 import TD3
from ml.replay_buffer import ReplayBuffer
from configs.parser import Parser
from assists.prepare_data import PrepareData
from assists.printer import Printer


if __name__ == "__main__":
    train_configs = Parser.parse_train_configs()
    data = PrepareData.read_data(train_configs.data_path, type="csv")
    env = Env.make(train_configs.env_name, data[0])

    # Set seeds
    env.set_seed(train_configs.seed)
    torch.manual_seed(train_configs.seed)
    np.random.seed(train_configs.seed)

    state_dim = env.get_state_dim()
    action_dim = env.get_action_dim()
    max_action = float(env.get_max_action())

    kwargs = {
        "state_dim": state_dim,
        "action_dim": action_dim,
        "max_action": max_action,
        "discount": train_configs.discount,
        "tau": train_configs.tau,
    }

    kwargs["policy_noise"] = train_configs.policy_noise * max_action
    kwargs["noise_clip"] = train_configs.noise_clip * max_action
    kwargs["policy_freq"] = train_configs.policy_freq
    policy = TD3(**kwargs)

    if train_configs.load_model:
        policy.load(train_configs.model_path+train_configs.file_name)

    replay_buffer = ReplayBuffer(state_dim, action_dim)

    # Evaluate untrained policy
    evaluations = [env.eval_policy(policy)]

    state, done = env.reset(), False
    episode_reward = 0
    episode_timesteps = 0
    episode_num = 0

    for t in range(int(train_configs.max_timesteps)):

        episode_timesteps += 1

        # Select action randomly or according to policy
        if t < train_configs.start_timesteps:
            action = env.sample_action()
        else:
            action = (
                policy.select_action(np.array(state))
                + np.random.normal(0, max_action *
                                   train_configs.expl_noise, size=action_dim)
            ).clip(-max_action, max_action)

        # Perform action
        next_state, reward, done = env.step(action)

        # Store data in replay buffer
        replay_buffer.add(state, action, next_state, reward, done)

        state = next_state
        episode_reward += reward

        # Train agent after collecting sufficient data
        if t >= train_configs.start_timesteps:
            policy.train(replay_buffer, train_configs.batch_size)

        if done:
            # +1 to account for 0 indexing. +0 on ep_timesteps since it will increment +1 even if done=True
            Printer.print_train(
                f"total T: {t+1} Episode Num: {episode_num+1} Episode T: {episode_timesteps} Reward: {episode_reward:.3f}")
            # Reset environment
            state, done = env.reset(), False
            episode_reward = 0
            episode_timesteps = 0
            episode_num += 1

        # Evaluate episode
        if (t + 1) % train_configs.eval_freq == 0:
            evaluations.append(env.eval_policy(policy))
            np.save(train_configs.result_path +
                    train_configs.file_name, evaluations)
            if train_configs.save_model:
                policy.save(train_configs.model_path+train_configs.file_name)
