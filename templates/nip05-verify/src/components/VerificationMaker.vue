<script setup>
import { ref, watch, computed, reactive } from 'vue';
import WelcomeItem from "./WelcomeItem.vue";
import CommunityIcon from "./icons/IconCommunity.vue";
import SupportIcon from "./icons/IconSupport.vue";

import { useVerificationStore } from "../stores/verification";
import { storeToRefs } from "pinia";

const store = useVerificationStore();

const { publicKey, username, domain, usernameCheckStatus, publicKeyCheckStatus } = storeToRefs(store);
const { checkUsername, checkPublicKey, submitToVerify } = store;

// local state
const showUsernameError = ref(false);
const publicKeyErrorMsg = ref('');
const verifyResult = reactive({
  nip05: ''
});


const showPublicKeyError = computed(() => publicKeyErrorMsg.value !== '');
const isSubmitBtnDisabled = computed(() => {
  if (showPublicKeyError.value || showUsernameError.value) {
    return true;
  }
  if (username.value === '' || publicKey.value === '' || domain.value === '') {
    return true;
  }
  if (verifyResult.nip05 !== '') {
    return true;
  }
  return false;
});
const showResult = computed(() => {
  return verifyResult.nip05 !== '';
});

function usernameChange(value) {
  checkUsername();
}

function publicKeyChange() {
  checkPublicKey();
}

function submit(v) {
  console.log(v)
  submitToVerify().then(data => {
    console.log('*********');
    console.log(data);
    console.log('*********');
    if (data.status === 'ok') {
      verifyResult.nip05 = data.nip05;
    }
  }).catch(error => {
    console.log(error);
  })
}

watch(usernameCheckStatus, async (newValue, oldValue) => {
  if (newValue === 'registered') {
    showUsernameError.value = true;
  } else {
    showUsernameError.value = false;
  }
});

watch(publicKeyCheckStatus, async (newValue, oldValue) => {
  if (newValue === 'format_error') {
    publicKeyErrorMsg.value = 'Your key is error, please confirm';
  } else if (newValue === 'registered') {
    publicKeyErrorMsg.value = 'Your key has been registered';
  }
  if (newValue === 'ok') {
    publicKeyErrorMsg.value = '';
  }
});

watch(verifyResult, async (newValue, oldValue) => {
  console.log(newValue, oldValue)
});

</script>

<template>
  <div class="maker-container">
    <h3>Pick a name to register.</h3>
    <div class="form-part-one">
      <div>
        <input id="username-input" placeholder="user" v-model="username" @change="usernameChange" />
        <div class="input-tip error-tip" v-show="showUsernameError">Username [{{ username }}] is registered</div>
      </div>
      @
      <div>
        <select id="domain-input" v-model="domain">
          <option value="workfun.life">workfun.life</option>
        </select>
      </div>
    </div>

    <h3>enter your <span class="important-tip">public</span> key</h3>
    <div>
      <input type="text" v-model="publicKey" placeholder="public key" @change="publicKeyChange" />
      <div class="input-tip error-tip" v-show="showPublicKeyError">{{ publicKeyErrorMsg }}</div>
    </div>
    <button :disabled="isSubmitBtnDisabled" @click="submit">Submit</button>
  </div>

  <Transition>
    <div class="result-container" v-show="showResult">
      <h3 class="center">🚀🚀🚀 Congratulations! 🎉🎉🎉</h3>
      <p>You have successfully registered for the verification service, only the last step...</p>
      <p>Now, please open your nostr client (such as Damus), please fill in the following information into the [Profile
        ->
        Edit -> NIP-05 VERIFICATION] form and save it.</p>
      <div class="nip05-info">
        <span>{{ verifyResult.nip05 }}</span>
      </div>
    </div>
  </Transition>

  <WelcomeItem>
    <template #icon>
      <CommunityIcon />
    </template>
    <template #heading>Community</template>

    Got stuck? Ask your question on Damus, My account:
    <code>npub10dnanfsan5y8q59y5gpv0jpgdntwjkrra0rukctpe3u2wvngfd5s2e7z9g</code>.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <SupportIcon />
    </template>
    <template #heading>Support Me</template>

    <div>If this gadget was helpful to you, you can help me by BitCoin Lighting!</div>
    <code
      class="code-warp">lnbc1p3alnevpp56pgu5xneldu2gsh0vsxwreal4l4u529u79ffpkfdmfrqtwtyk4wsdpz235xzmntwvsxvmmjypuk7atjyp4kjmnyyycqzpgxqyz5vqsp5u0sruvkjv5y4rll5cw4an2j39e7gsyljc6un2x9curg5qcvxmvdq9qyyssq320rme49cl4rt9s3dppv04dr6ssexvzllw228z24g4fy5324s07xwgjp2cc2l7the7cf9n28mp2z9vwvyc0lp9ckyszrfuyth9um67cq66yayu</code>
    Or
    <div>
      <img alt="Damus logo" class="qr-code" src="@/assets/lighting-qr.png" width="125" height="125" />
    </div>

  </WelcomeItem>
</template>

<style scoped>
h3 {
  padding-bottom: 0.4rem;
}

.maker-container {}

.form-part-one {
  display: flex;
}

#username-input {
  margin-right: 1rem;
}

#domain-input {
  margin-left: 1rem;
}

.important-tip {
  font-weight: 600;
}

.input-tip {
  margin-bottom: 1rem;
}

.error-tip {
  color: rgb(204, 40, 40);
}

.result-container {
  margin-top: 2rem;
  margin-bottom: 4rem;
}

.nip05-info {
  text-align: center;
  transition: 0.3s;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  padding: 1rem;
}

.center {
  text-align: center;
}

.code-warp {
  overflow-wrap: anywhere;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.qr-code {
  display: block;
  margin: 0 5rem;
}
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>