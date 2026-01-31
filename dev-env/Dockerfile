FROM nixos/nix:latest

RUN mkdir -p ~/.config/nix && \
    echo "experimental-features = nix-command flakes" > ~/.config/nix/nix.conf

RUN nix-channel --update

# Copy shell.nix to /etc
COPY shell.nix /etc/shell.nix

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Pre-build the nix-shell environment
RUN cd /etc && nix-shell --run "uv --version"

WORKDIR /workspace

ENTRYPOINT ["nix-shell", "/etc/shell.nix", "--run"]
CMD ["/usr/local/bin/entrypoint.sh"]
