import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useVerificationStore = defineStore("verification", {
  state: () => ({
    publicKey: '',
    username: '',
    domain: 'workfun.life',
    usernameCheckStatus: '',
    publicKeyCheckStatus: ''
  }),
  getters: {
  },
  actions: {
    async checkUsername() {
      try {
        const data = await fetch('/api/username/' + this.username + '/-/action/check')
        .then((response) => response.json());
        console.log(data);
        console.log(data.status);
        this.usernameCheckStatus = data.status;
      } catch (error) {
        console.error(error)
      }
    },
    async checkPublicKey() {
      try {
        const data = await fetch('/api/publickey/' + this.publicKey + '/-/action/check')
        .then((response) => response.json());
        console.log(data);
        console.log(data.status);
        this.publicKeyCheckStatus = data.status;
      } catch (error) {
        console.error(error)
      }
    },
    async submitToVerify() {
      const payload = {
        'username': this.username,
        'public_key': this.publicKey,
        'domain': this.domain,
      }
      try {
        const data = fetch('/api/verify', {
          method: 'POST',
          body: JSON.stringify(payload),
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then((response) => response.json());
        console.log(data);
        return data;
      } catch (error) {
        console.error(error)
        return error;
      }
    }
  }
});
